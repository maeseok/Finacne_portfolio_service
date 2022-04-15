const ID = document.getElementById("id");
const PWD = document.getElementById("pwd");
const PWD2 = document.getElementById("pwd2");
const NICK = document.getElementById("nick");
const regul1 = /^[a-zA-Z0-9]{4,12}$/;

/*
if (ID.value == "") {
  alert("아이디를 입력하지 않았습니다.");
  ID.focus();
  return false;
} else if (PWD.value == "" || PWD2.value == "") {
  alert("비밀번호를 입력하지 않았습니다.");
  PWD.focus();
  return false;
} else if (NICK.value == "") {
  alert("닉네임을 입력하지 않았습니다.");
  NICK.focus();
  return false;
}*/

if (
  !check(regul1, ID, "아이디는 4~12자의 대소문자와 숫자로만 입력 가능합니다.")
) {
  return false;
}
if (
  !check(
    regul1,
    PWD,
    "비밀번호는 4~12자의 대소문자와 숫자로만 입력 가능합니다."
  )
) {
  return false;
}
