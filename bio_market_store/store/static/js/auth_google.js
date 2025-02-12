// const google_login = () => {
//   let pop_up = window.open(
//     "/accounts/google/login/?process=login",
//     "google_login",
//     "width=800, height=600"
//   );

//   let interval = setInterval(() => {
//     if (pop_up.closed) {
//       clearInterval(interval);
//       location.reload();
//     }
//   }, 1000);
// };
const google_login = () => {
  if (window.google) {
    window.google.accounts.id.initialize({
      client_id: document
        .getElementById("g_id_onload")
        .getAttribute("data-client_id"),
      callback: handleCredentialResponse,
    });

    window.google.accounts.id.renderButton(
      document.querySelector(".g_id_signin"),
      {
        theme: "outline",
        size: "large",
      }
    );
  } else {
    console.error("Google API is not loaded.");
  }
};

const handleCredentialResponse = (response) => {
  console.log("Credential Response:", response);
}
