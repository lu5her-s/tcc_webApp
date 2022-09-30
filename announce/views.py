from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from account.models import LineToken

from announce.forms import AnnounceForm
from announce.models import (
    Announce,
    AnnounceFile,
    AnnounceImage,
    Comment
)

# from app_config.sendline import Sendline

# Create your views here.

def AnnounceRead(request, pk):
    announce = get_object_or_404(Announce, pk=request.POST.get('announce_id'))
    if announce.reads.filter(id=request.user.id).exists():
        announce.reads.remove(request.user)
    else:
        announce.reads.add(request.user)
    # return HttpResponseRedirect(reverse_lazy('announce:detail', args=(announce.pk)))
    return HttpResponseRedirect(reverse_lazy('announce:detail', args=[str(pk)]))

class AnnounceListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model               = Announce
    template_name       = 'announce/announce.html'
    # context_object_name = 'announce_list'
    paginate_by         = 20
    ordering            = ('-created_at')

    def get_context_data(self, **kwargs):
        context          = super(AnnounceListView, self).get_context_data(**kwargs)
        context['read']  = Announce.objects.filter(reads__id=self.request.user.id)
        context['title'] = "ประชาสัมพันธ์"
        return context

def announce_read(request, pk):
    announce = get_object_or_404(Announce, pk=request.POST.get('announce_id'))
    if announce.reads.filter(id=request.user.id).exists():
        announce.reads.remove(request.user)
    else:
        announce.reads.add(request.user)
    return HttpResponseRedirect(reverse_lazy('announce:detail', args=[str(pk)]))

class AnnounceDetailView(LoginRequiredMixin, DetailView):
    login_url     = reverse_lazy('login')
    template_name = 'announce/detail.html'
    model         = Announce
    # context_object_name = 'announce'

    def get_context_data(self, **kwargs):
        context = super(AnnounceDetailView, self).get_context_data(**kwargs)

        read_connected = get_object_or_404(Announce, pk=self.object.pk)
        read           = False
        if read_connected.reads.filter(id=self.request.user.id).exists():
            read = True

        context['images']           = AnnounceImage.objects.filter(announce=self.object)
        context['files_list']       = AnnounceFile.objects.filter(announce=self.object)
        context['number_of_reader'] = read_connected.number_of_reader()
        context['is_read']          = read
        context['comments']         = Comment.objects.filter(announce=self.object)
        context['comments_count']   = Comment.objects.filter(announce=self.object).count()

        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context     = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object  = self.get_object()
        context      = self.get_context_data(object=self.object)
        comment      = self.request.POST.get('comment', None)
        announce_id  = self.request.POST.get('announce_id')
        comment_save = Comment.objects.create(announce=self.object, comment=comment, author=self.request.user)
        comment_save.save()
        return HttpResponseRedirect(self.request.path_info)

class AnnounceCreateView(LoginRequiredMixin, CreateView):
    login_url     = reverse_lazy('login')
    template_name = 'announce/announce_form.html'
    form_class    = AnnounceForm
    success_url   = reverse_lazy('announce:list')

    def get(self, request, *args, **kwargs):
        context = {
            'form'     : self.form_class,
            'title'    : 'Create',
            'header'   : 'สร้างประชาสัมพันธ์/สั่งการ',
            'btn_text' : 'สร้าง'
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            images    = request.FILES.getlist('images')
            files     = request.FILES.getlist('files')
            tokens    = request.POST.getlist('tokens')
            form_save = form.save()
            form_id   = get_object_or_404(Announce, pk=form_save.pk)

            if images:
                for image in images:
                    a_image = AnnounceImage(announce=form_id, images=image)
                    a_image.save()
            else:
                form_save.save()

            if files:
                for f in files:
                    a_file = AnnounceFile(announce=form_id, files=f)
                    a_file.save()
            else:
                form_save.save()

            if tokens:
                host = request.get_host()
                path = reverse_lazy('announce:detail', args=[str(form_id.pk)])
                url  = 'http://' + host + path
                head = '\nมี : ' + form_save.is_type.name + 'ใหม่'
                body = '\nเรื่อง : ' + form_save.name + '\n' + 'รายละเอียดเพิ่มเติม :' + url

                for token_id in tokens:
                    token = LineToken.objects.get(id=token_id).token
                    line  = Sendline(token)
                    line.sendtext(head + body)
                    # print(token)

            return redirect(self.success_url)

        else:
            form = self.form_class()

        context = {
            'form'     : form,
            'title'    : 'Create',
            'header'   : 'สร้างประชาสัมพันธ์/สั่งการ',
            'btn_text' : 'สร้าง'
        }
        return render(request, self.template_name, context)

class AnnounceUpdateView(LoginRequiredMixin, UpdateView):
    login_url     = reverse_lazy('login')
    template_name = 'announce/announce_form.html'
    model         = Announce
    form_class    = AnnounceForm
    pk            = None
    success_url   = reverse_lazy('announce:list')

    def get_success_url(self):
        return reverse('announce:detail', kwargs={'pk': self.pk})


    def get(self, request, *args, **kwargs):
        form   = self.form_class(instance=self.get_object())
        images = AnnounceImage.objects.filter(announce=self.get_object())
        files  = AnnounceFile.objects.filter(announce=self.get_object())

        context = {
            'form'     : form,
            'images'   : images,
            'files'    : files,
            'title'    : 'Update',
            'header'   : 'อัพเดทประชาสัมพันธ์/สั่งการ',
            'btn_text' : 'อัพเดท'
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=self.get_object())

        if form.is_valid():
            images    = request.FILES.getlist('images')
            files     = request.FILES.getlist('files')
            form_save = form.save()
            form_id   = get_object_or_404(Announce, pk=form_save.pk)

            if images:
                for image in images:
                    a_image = AnnounceImage.objects.create(announce=form_id, images=image)
                    a_image.save()
            else:
                form_save.save()

            if files:
                for file in files:
                    try:
                        a_file = InboxFile.objects.get(inbox=form_id)
                        a_file.files = file
                        a_file.save()
                    except ObjectDoesNotExist:
                        a_file = InboxFile.objects.create(inbox=form_id, files=file)
                        a_file.save()
            else:
                form_save.save()

        else:
            form = self.form_class(instance=self.get_object())

        return redirect(self.success_url)

class AnnounceNotReadView(LoginRequiredMixin, ListView):
    login_url     = reverse_lazy('login')
    model         = Announce
    template_name = 'announce/announce.html'
    # context_object_name = 'announce_list'
    paginate_by   = 20
    ordering      = ('-created_at')

    def get_queryset(self):
        # return super().get_queryset()
        qs = Announce.objects.filter(~Q(author=self.request.user) & ~Q(reads__id=self.request.user.id))
        return qs

    def get_context_data(self, **kwargs):
        context             = super(AnnounceNotReadView, self).get_context_data(**kwargs)
        context['not_read'] = self.request.user.announce_set.filter(~Q(author=self.request.user) & Q(reads__id=self.request.user.id)).count()
        context['header']   = "ยังไม่ได้อ่าน"
        return context

class AnnounceDeleteView(LoginRequiredMixin, DeleteView):
    login_url     = reverse_lazy('login')
    template_name = 'announce/announce_delete.html'
    model         = Announce
    success_url   = reverse_lazy('announce:list')

    def get_context_data(self, **kwargs):
        context             = super().get_context_data(**kwargs)
        context['header']   = 'ยืนยันการลบ'
        context['btn_text'] = 'ลบ'
        return context

def my_announce(request, user):
    qs = Announce.objects.filter(author=user)
    return render(request, 'announce/annoucne.html', {'object_list': qs})
