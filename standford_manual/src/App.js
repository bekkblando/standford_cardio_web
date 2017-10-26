import React, { Component } from 'react';
import logo from './logo.svg';
import TinyMCE from 'react-tinymce';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);

    // This binding is necessary to make `this` work in the callback
    this.save_manual = this.save_manual.bind(this);
  }

  save_manual(){
    this.props.manual_ref.set(document.getElementById("manual").innerHTML);
  }

  render() {

    // Output TinyMCE if successful
    return (
      <div>
        <button id="save_manual" onClick={this.save_manual}>Save Manual</button>
        <div contentEditable id="manual">Manual Loading</div>
      </div>
    );
  }
}

export default App;
