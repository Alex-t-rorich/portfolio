function deleteEducation(educationId) {
    fetch("/delete-education", {
      method: "POST",
      body: JSON.stringify({ educationId: educationId }),
    }).then((_res) => {
      window.location.href = "/admin";
    });
  }