$(document).ready(function () {
  $(".radio-list li label").click(function () {
    var list = $(".radio-list li");
    var thisList = $(this).parent("li");
    var checkRadio = $(this).children("input").is(":checked"); //체크유무 (체크면 true, 아니면 false)

    if (checkRadio == true) {
      list.removeClass("active");
      thisList.addClass("active");
    } else {
      list.removeClass("active");
      thisList.removeClass("active");
    }
  });
});
