function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}


function deleteform(formId) {
  fetch("/delete_forms", {
    method: "POST",
    body: JSON.stringify({ formId: formId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}


function viewform(formId) {
  fetch("/view-form", {
    method: "POST",
    body: JSON.stringify({ formId: formId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}


function deletequestion(dataaId) {
  fetch("/delete_question", {
    method: "POST",
    body: JSON.stringify({ dataaId : dataaId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function deletequestion1(dataaId,formname) {
  fetch("/delete_question", {
    method: "POST",
    body: JSON.stringify({ dataaId : dataaId }),
  }).then((_res) => {
    window.location.href = "/view/<formname>";
  });
}

