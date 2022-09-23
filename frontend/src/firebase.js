// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCJQRB1bSfEJ4LuNhUf0SoQ7OaLFRsvqk4",
  authDomain: "youtify-357009.firebaseapp.com",
  projectId: "youtify-357009",
  storageBucket: "youtify-357009.appspot.com",
  messagingSenderId: "197724356935",
  appId: "1:197724356935:web:ff2f056fd44312f1918c62",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

const auth = getAuth(app);

export default auth;
