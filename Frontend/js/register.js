const form = document.getElementById("registerForm");
const message = document.getElementById("message");

form.addEventListener("submit",function(e){
   e.preventDefault(); 

  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!name || !email || !password) {
    message.textContent = "All fields are required";
    message.style.color = "red";
    return;
  }
    if (!email.includes("@")) {
    message.textContent = "Invalid email";
    message.style.color= "red";
    return;
    }


  if (password.length < 6) {
    message.textContent = "password must be at least 6 characters";
    message.style.color = "red";
    return;
  }
  registerUser(name, email, password);

});

function registerUser(name,email,password){
    fetch("http://localhost:5000/auth/register",
        {
        method: "POST",
        headers:{
            "Content-Type": "application/json"

        },
        body: JSON.stringify({
            name: name,
            email: email,
            password: password
        })

    })
    .then(response => response.json())
    .then(data => {
        if(data.message){
            message.textContent = data.message;
            message.style.color = "green";

            form.reset();
        } else if (data.error) {
   
      message.textContent = data.error;
      message.style.color = "red";
    }
    })
    .catch(error => {
         message.textContent = "Server error. Try again later.";
        message.style.color = "red";
        console.error(error);
    })
}
