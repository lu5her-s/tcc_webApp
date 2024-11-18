# Asset Management Documentation

## Stock Item Views

- **StockItemListView**: แสดงรายการ StockItem ทั้งหมด
- **StockItemDetailView**: แสดงรายละเอียดของ StockItem เฉพาะ
- **StockDepartmentListView**: แสดงรายการ StockItem ตามแผนกของผู้ใช้
- **StockItemHomeView**: แสดงหน้าแรกของแอปพลิเคชัน Asset
- **StockItemCreateView**: อนุญาตให้ผู้ใช้สร้าง StockItem ใหม่
- **StockItemUpdateView**: อนุญาตให้ผู้ใช้แก้ไข StockItem ที่มีอยู่
- **StockItemDeleteView**: อนุญาตให้ผู้ใช้ลบ StockItem
- **set_item**: อัปเดตสถานะของ StockItem เป็น IN_USE และตั้งค่าตำแหน่งของ StockItem
- **remove_item**: อัปเดตสถานะของ StockItem เป็น AVAILABLE

## Stock Manager Views

- **StockManageHomeView**: แสดงหน้าแรกสำหรับผู้จัดการคลังพัสดุ
- **StockManagerListView**: แสดงรายการ StockItem ตามกลุ่มของผู้ใช้
- **categories_list**: แสดงรายการ StockItem ตามหมวดหมู่ที่ระบุ
- **manufacturer_list**: แสดงรายการ StockItem ตามผู้ผลิตที่ระบุ
- **network_list**: แสดงรายการ StockItem ตามเครือข่ายที่ระบุ

## Stock models

- **Category**: หมวดหมู่ของพัสดุ
- **Supplier**: ผู้จำหน่ายพัสดุ
- **Network**: เครือข่ายที่เกี่ยวข้องกับพัสดุ
- **Manufacturer**: ผู้ผลิตพัสดุ
- **StockItem**: รายละเอียดของพัสดุ
- **StockItemImage**: รูปภาพของพัสดุ
- **ItemLocation**: ตำแหน่งของพัสดุ
- **ItemOnHand**: ผู้ใช้ที่ถือครองพัสดุ
- **ItemHistory**: ประวัติการใช้งานของพัสดุ

## URLS patterns

- path("", views.StockItemHomeView.as_view(), name="stockitem_home"),: แสดงหน้าแรกของแอปพลิเคชัน Asset
- path("list/", views.StockItemListView.as_view(), name="stockitem_list"),: แสดงรายการ StockItem ทั้งหมด
- path("<int:pk>/", views.StockItemDetailView.as_view(), name="stockitem_detail"),: แสดงรายละเอียดของ StockItem เฉพาะ
- path("add-item/", views.StockItemCreateView.as_view(), name="stockitem_create"),: อนุญาตให้ผู้ใช้สร้าง StockItem ใหม่
- path("update/<int:pk>/", views.StockItemUpdateView.as_view(), name="stockitem_update"),: อนุญาตให้ผู้ใช้แก้ไข StockItem ที่มีอยู่
- path("manager/home/", views.StockManageHomeView.as_view(), name="manager_home"),: แสดงหน้าแรกสำหรับผู้จัดการคลังพัสดุ
- path("manager/list/", views.StockManagerListView.as_view(), name="manager_list"),: แสดงรายการ StockItem ตามกลุ่มของผู้ใช้
- path("category/<int:pk>/", views.categories_list, name="category_list"),: แสดงรายการ StockItem ตามหมวดหมู่ที่ระบุ
- path("manufacturer/<int:pk>/", views.manufacturer_list, name="manufacturer_list"),: แสดงรายการ StockItem ตามผู้ผลิตที่ระบุ
- path("network/<int:pk>/", views.network_list, name="network_list"),: แสดงรายการ StockItem ตามเครือข่ายที่ระบุ
- path("department/list/", views.StockDepartmentListView.as_view(), name="department_list",),: แสดงรายการ StockItem ตามแผนกของผู้ใช้
- path("delete/<int:pk>/", views.StockItemDeleteView.as_view(), name="stockitem_delete"),: อนุญาตให้ผู้ใช้ลบ StockItem

## Flow Diagram

# URL patterns for StockItem management

| URL Path             | View Function                    | Description                                                                 |
|----------------------|---------------------------------|-----------------------------------------------------------------------------|
| `/`                  | `StockItemHomeView`             | Displays the Asset application's home page.                               |
| `/list/`             | `StockItemListView`             | Displays a list of all StockItems.                                         |
| `/<int:pk>/`         | `StockItemDetailView`            | Displays details for a specific StockItem (identified by `pk`).           |
| `/add-item/`         | `StockItemCreateView`           | Allows users to create a new StockItem.                                    |
| `/update/<int:pk>/`  | `StockItemUpdateView`           | Allows users to update an existing StockItem (identified by `pk`).        |
| `/manager/home/`     | `StockManageHomeView`           | Displays the home page for Stock managers.                                |
| `/manager/list/`    | `StockManagerListView`          | Displays a list of StockItems based on the user's group.                  |
| `/category/<int:pk>/` | `categories_list`              | Displays a list of StockItems filtered by a specific category (identified by `pk`). |
| `/manufacturer/<int:pk>/` | `manufacturer_list`          | Displays a list of StockItems filtered by a specific manufacturer (identified by `pk`). |
| `/network/<int:pk>/` | `network_list`                 | Displays a list of StockItems filtered by a specific network (identified by `pk`). |
| `/department/list/` | `StockDepartmentListView`       | Displays a list of StockItems filtered by the user's department.         |
| `/delete/<int:pk>/`  | `StockItemDeleteView`           | Allows users to delete a StockItem (identified by `pk`).                  |
