function deleteNav(navId) {
    fetch("/delete-nav", {
      method: "POST",
      body: JSON.stringify({ navId: navId }),
    }).then((_res) => {
      window.location.href = "/admin";
    });
  }