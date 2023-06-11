<script>

import { getAuth, onAuthStateChanged } from "firebase/auth";

export default {
    name: "Api",
    props: {
        msg: String,
    },
    data() {
        return {
            text: null,
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
            } else {
                // User is signed out
                // ...
                console.log("Failed to fetch the user data.");
            }
        });

        // fetch the data from fast api
        axios.get("user_info").then(
            (response) => (this.text = response.data)
        ).catch(
            (e) => console.log(e)
        );
    },
    methods: {
    },
}

</script>


<template>
    <h3>User specific data</h3>
    <br />
    <h4>User name: {{ user_name }}</h4>
    <br />
    <h4>User id: {{ user_id }}</h4>
    <br />
    <h4>User data: {{ text }}</h4>
</template>
