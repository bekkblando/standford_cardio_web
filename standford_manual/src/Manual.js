import firebase from './init_firebase';
import React, { Component } from 'react';

class Manual extends Component {
  constructor(props) {
    super(props);

    // This binding is necessary to make `this` work in the callback
    this.save_manual = this.save_manual.bind(this);
  }

  save_manual(){
    this.props.manual_ref.set(document.getElementById("manual").innerHTML);
  }

  render() {

    // Get the manual
    var manual_ref = firebase.database().ref().child("manual");

    manual_ref.on("value", function(manual) {
      var output_text = manual.val();

      // Not an ideal way of loading the manual
      document.getElementById("manual").innerHTML = output_text;

    }, function (errorObject) {
      // Failed
      console.log("The read failed: " + errorObject.code);
    });

    // Output TinyMCE if successful
    return (
      <div>
        <button id="save_manual" onClick={this.save_manual}>Save Manual</button>
        <div contentEditable id="manual">Manual Loading</div>
      </div>
    );
  }
}

export default Manual;
