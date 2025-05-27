function doPost(e) {
  var LINE_REPLY_URL = "https://api.line.me/v2/bot/message/reply";
  var CHANNEL_ACCESS_TOKEN = "YOUR_LINE_CHANNEL_ACCESS_TOKEN"; // <-- Set your token here

  // Parse the request body
  var event = JSON.parse(e.postData.contents).events[0];
  var replyToken = event.replyToken;
  var userId = event.source.userId;

  // Call TCC web app for not read announces
  var tccUrl = "http://localhost:8000/api/announce?userId=" + encodeURIComponent(userId);
  var announceRes = UrlFetchApp.fetch(tccUrl, { muteHttpExceptions: true });
  var announces = JSON.parse(announceRes.getContentText());

  // Format announce message
  var announceMsg = announces.length > 0
    ? announces.map(function (a, i) { return (i + 1) + ". " + a.title; }).join("\n")
    : "No new announcements.";

  // Prepare reply body
  var payload = JSON.stringify({
    replyToken: replyToken,
    messages: [{ type: "text", text: announceMsg }]
  });

  // Reply to LINE user
  UrlFetchApp.fetch(LINE_REPLY_URL, {
    method: "post",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + CHANNEL_ACCESS_TOKEN
    },
    payload: payload
  });

  return ContentService.createTextOutput("OK");
}

function doGet() {
  return ContentService.createTextOutput("OK");
}
