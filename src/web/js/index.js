function getJsonValueFromForm() {
  const formElement = document.querySelector("form");
  const formData = new FormData(formElement);
  var object = {};
  formData.forEach(function (value, key) {
    object[key] = value;
  });
  var json = JSON.stringify(object);
  console.log(json);
  return json;
}

$(document).ready(function () {
  function dropHandler(ev) {
    console.log("drop");
    ev.preventDefault();
    if (ev.dataTransfer.items) {
      let ff = new DataTransfer();
      // Use DataTransferItemList interface to access the file(s)
      [...ev.dataTransfer.items].forEach((item, i) => {
        // If dropped items aren't files, reject them
        if (item.kind === "file") {
          const file = item.getAsFile();
          console.log(`… file[${i}].name = ${file.name}`);
          ff.items.add(file);
        }
      });
      document.getElementById("file").files = ff.files;
    } else {
      let ff = new DataTransfer();
      // Use DataTransfer interface to access the file(s)
      [...ev.dataTransfer.files].forEach((file, i) => {
        ff.items.add(file);
        console.log(`… file[${i}].name = ${file.name}`);
      });
      document.getElementById("file").files = ff.files;
    }
  }

  window.addEventListener(
    "dragover",
    function (e) {
      e.preventDefault();
    },
    false
  );
  window.addEventListener(
    "drop",
    function (e) {
      e.preventDefault();
    },
    false
  );

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
      var myFile = document.getElementById("file").files[0];
      console.log(document.getElementById("file"));
      if (myFile) {
        const reader = new FileReader();
        reader.onload = function (evt) {
          const metadata = `name: ${myFile.name}, type: ${myFile.type}, size: ${myFile.size}, contents:`;
          const content = evt.target.result;
          let json = getJsonValueFromForm();
          eel.getFormData(json, metadata, content);
        };
        reader.readAsBinaryString(myFile);
      } else {
        console.log("empty file");
        let json = getJsonValueFromForm();
        eel.getFormData(json);
      }
      //TODO: go to result page
      $(document).find(".form-wrapper .section").first().addClass("is-active");
      $(document).find(".steps li").first().addClass("is-active");
    }
  });

  $("#tlefile").change(function () {
    if (this.checked) {
      console.log("checked");
      $("#constellation-page input:text").prop("disabled", true);
      $("#constellation-page input:text").addClass("deactive-label");
      $("#constellation-page input:file").prop("disabled", false);
      $("#constellation-page input:file").removeClass("deactive-label");
    } else {
      $("#constellation-page input:text").prop("disabled", false);
      $("#constellation-page input:text").removeClass("deactive-label");
      $("#constellation-page input:file").prop("disabled", true);
      $("#constellation-page input:file").addClass("deactive-label");
    }
  });

  $(".steps li").click(function () {
    var index = $(this).index();
    $(".steps li").removeClass("is-active");
    $(".section").removeClass("is-active");
    $(".section").eq(index).addClass("is-active");
    $(this).addClass("is-active");
  });

  document.querySelectorAll(".drop-container").forEach(function (dc) {
    console.log("event added");
    dc.addEventListener("drop", dropHandler);
  });
});
