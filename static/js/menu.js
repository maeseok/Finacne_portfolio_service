$(document).ready(function () {
  $("#inqu-menu").hide();
  $("#port-menu").hide();
  $("#init-menu").hide();

  $("#inqu").mouseover(function () {
    $("#inqu-menu").slideDown();
  });
  $("#inqu").mouseleave(function () {
    $("#inqu-menu").hide();
  });
  $("#port").mouseover(function () {
    $("#port-menu").slideDown();
  });
  $("#port").mouseleave(function () {
    $("#port-menu").hide();
  });
  $("#init").mouseover(function () {
    $("#init-menu").slideDown();
  });
  $("#init").mouseleave(function () {
    $("#init-menu").hide();
  });
});
