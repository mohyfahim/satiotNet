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

function getBinaryStringFromFile(file) {
  return new Promise((resolve) => {
    console.log("start promise");
    const reader = new FileReader();
    reader.onload = function (evt) {
      console.log("start promise4");

      const metadata = { name: file.name, type: file.type, size: file.size };
      const content = evt.target.result;
      resolve({ meta: metadata, content: content });
    };
    console.log("start promise2");
    console.log(file);
    reader.readAsBinaryString(file);
    console.log("start promise3");
  });
}

$(document).ready(function () {
  function dropHandler(ev) {
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
      ev.target.querySelector("input[type=file]").files = ff.files;
    } else {
      let ff = new DataTransfer();
      // Use DataTransfer interface to access the file(s)
      [...ev.dataTransfer.files].forEach((file, i) => {
        ff.items.add(file);
        console.log(`… file[${i}].name = ${file.name}`);
      });
      ev.target.querySelector("input[type=file]").files = ff.files;
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

  $(".form-wrapper .button").click(async function () {
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
      console.log("start");
      let files = document.querySelectorAll("input[type=file]");
      let sendFile = [];
      for (let i = 0; i < files.length; i++) {
        if (files[i].files[0]) {
          let key = files[i].name;
          let bfile = await getBinaryStringFromFile(files[i].files[0]);
          sendFile.push({ key: key, file: bfile });
        }
      }
      console.log("end");

      let json = getJsonValueFromForm();
      eel.getFormData(json, JSON.stringify(sendFile));
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
