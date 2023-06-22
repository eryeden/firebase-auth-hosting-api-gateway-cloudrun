<script>

import {getAuth, onAuthStateChanged} from "firebase/auth";
import {axios} from "@/plugins/axios"
// import axios from 'axios'
// import VueAxios from 'vue-axios'


export default {
  name: "Api",
  props: {
    msg: String,
  },
  data() {
    return {
      special_message: null,
      greeting_message: null,
      user_name: "",
      user_id: ""
    }
  },
  mounted() {
    const auth = getAuth();
    // fetch the username and user id using the firebase api
    onAuthStateChanged(auth, (user) => {
      if (user) {
        // The user object has basic properties such as display name, email, etc.
        const displayName = user.displayName;
        const email = user.email;
        const photoURL = user.photoURL;
        const emailVerified = user.emailVerified;
        // The user's ID, unique to the Firebase project. Do NOT use
        // this value to authenticate with your backend server, if
        // you have one. Use User.getToken() instead.
        const uid = user.uid;
        this.user_id = uid;
        this.user_name = displayName;
        console.log("User data:" + this.user_id);

        // fetch the special_message with authentication from fast api
        auth.currentUser?.getIdToken(false).then(
            (idToken) => {
              console.log("ID token: " + idToken)

              axios.get("special_message", {
                headers: {
                  "Authorization": "Bearer " + idToken
                }
              }).then(
                  (response) => {
                    console.log("API response:[/special_message]" + response)
                    this.special_message = response.data
                  }
              ).catch(
                  (error) => {
                    console.log("Error API response:[/special_message]" + error)
                  }
              )
            })

      } else {
        // User is signed out
        // ...
        console.log("Failed to fetch the user data.");
      }
    });

    // // fetch the data from fast api
    axios.get("/greeting_message").then(
        (response) => (this.greeting_message = response.data)
    ).catch(
        (e) => console.log(e)
    );


    // axios.get("special_message").then(
    //     (response) => (this.special_message = response.data)
    // ).catch(
    //     (e) => console.log(e)
    // );

  },
  methods: {}
}

</script>


<template>
  <h3>User specific data</h3>
  <br/>
  <h4>User name: {{ user_name }}</h4>
  <br/>
  <h4>User id: {{ user_id }}</h4>
  <br/>
  <h4>Special message: {{ special_message }}</h4>
  <br/>
  <h4>Greeting message: {{ greeting_message }}</h4>
</template>
