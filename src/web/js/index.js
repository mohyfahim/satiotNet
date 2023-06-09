

var resultFileD = "";

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
function selectFolder(e) {
  var theFiles = e.target.files;
  var relativePath = theFiles[0].webkitRelativePath;
  var folder = relativePath.split("/");
  resultFileD = folder[0];
  console.log(resultFileD);
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

    $(".form-wrapper").submit(function (e) {
      e.preventDefault();
    });

    if (currentSectionIndex === 2) {
      currentSection.removeClass("is-active").next().addClass("is-active");
      headerSection.removeClass("is-active").next().addClass("is-active");
  
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
      let resp = await eel.getFormData(json, JSON.stringify(sendFile))();
      alert(resp);
      //TODO: go to result page
      // $(document).find(".form-wrapper .section").first().addClass("is-active");
      // $(document).find(".steps li").first().addClass("is-active");
    }else if (currentSectionIndex === 3){
      console.log("res");
      let json = getJsonValueFromForm();
      $(".lds-ring").show();
      let resp = await eel.getResults(resultFileD, json)();
      alert(resp);
      $(".lds-ring").hide();

      // $('iframe').attr('src', "file://" + resp);
      // $("iframe").show();

    }
  });

  $("#tlefile").change(function () {
    if (this.checked) {
      console.log("checked");
      $("#constellation-page input:text").prop("disabled", true);
      $("#constellation-page input:text").addClass("deactive-label");
      $('#constellation-page input[type="number"]').prop("disabled", true);
      $('#constellation-page input[type="number"]').addClass("deactive-label");
      $("#constellation-page #PHASE_DIFF").prop("disabled", true);
      $("#constellation-page #PHASE_DIFF").addClass("deactive-label");

      $("#constellation-page input:file").prop("disabled", false);
      $("#constellation-page input:file").removeClass("deactive-label");
    } else {
      $("#constellation-page input:text").prop("disabled", false);
      $("#constellation-page input:text").removeClass("deactive-label");
      $('#constellation-page input[type="number"]').prop("disabled", false);
      $('#constellation-page input[type="number"]').removeClass("deactive-label");
      $("#constellation-page #PHASE_DIFF").prop("disabled", false);
      $("#constellation-page #PHASE_DIFF").removeClass("deactive-label");
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

  $("#rlAlgo input:checkbox").on('click', function() {
    // in the handler, 'this' refers to the box clicked on
    var $box = $(this);
    if ($box.is(":checked")) {
      // the name of the box is retrieved using the .attr() method
      // as it is assumed and expected to be immutable
      var group = "#rlAlgo input:checkbox";
      // the checked state of the group/box on the other hand will change
      // and the current value is retrieved using .prop() method
      $(group).prop("checked", false);
      $box.prop("checked", true);
    } else {
      $box.prop("checked", false);
    }
  });
});
