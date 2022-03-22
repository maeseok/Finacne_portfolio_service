$(function () {
  //화면 로딩후 시작
  $("#stock-input").autocomplete({
    //오토 컴플릿트 시작
    //최대 출력 개수 100로 제한
    maxResults: 100,
    source: function (request, response) {
      var results = $.ui.autocomplete.filter(List, request.term);
      response(results.slice(0, this.options.maxResults));
    },
    focus: function (event, ui) {
      // 방향키로 자동완성단어 선택 가능하게 만들어줌
      return false;
    },
    minLength: 1, // 최소 글자수
    delay: 100, //autocomplete 딜레이 시간(ms)
    //disabled: true, //자동완성 기능 끄기
  });
});
