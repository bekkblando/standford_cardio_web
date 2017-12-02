// Simulates server calls
import firebase from '../init_firebase.js';

export const login = (user) => {

  var response = {
    token: 0,
    data: "Invalid User"
  }

  firebase.auth().signInWithEmailAndPassword(user.email,
    user.password).catch(function(error) {
      // Handle Errors here.
      var errorCode = error.code;
      var errorMessage = error.message;
      if (errorCode === 'auth/wrong-password') {
        alert('Wrong password.');
      } else {
        alert(errorMessage);
      }
      console.log(error);
  });

  var current_user = firebase.auth().currentUser;
  if(current_user){
    response = {
      token: current_user.uid,
      email: current_user.email,
      first: current_user.displayName
    }
  }else{
    response = {
      token: 0,
      email: 'Invalid'
    }
  }
  console.log(response)
  return new Promise(resolve => setTimeout(resolve(response), 1000));

};

export const logout = () => {
  if(firebase.auth().currentUser){
    firebase.auth().signOut();
  }
  return new Promise(resolve => setTimeout(resolve, 1000));
};
