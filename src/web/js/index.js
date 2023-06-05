$(document).ready(function () {
  $(".form-wrapper .button").click(function () {
    var button = $(this);
    var currentSection = button.parents(".section");
    var currentSectionIndex = currentSection.index();
    var headerSection = $(".steps li").eq(currentSectionIndex);
    currentSection.removeClass("is-active").next().addClass("is-active");
    headerSection.removeClass("is-active").next().addClass("is-active");

    $(".form-wrapper").submit(function (e) {
      e.preventDefault();
    });

    if (currentSectionIndex === 3) {
      eel.say_hello_py("ass");
      console.log("asb");
      $(document).find(".form-wrapper .section").first().addClass("is-active");
      $(document).find(".steps li").first().addClass("is-active");
    }
  });
});

$(".steps li").click(function () {
  var index = $(this).index();
  $(".steps li").removeClass("is-active");
  $(".section").removeClass("is-active");
  $(".section").eq(index).addClass("is-active");
  $(this).addClass("is-active");
});
