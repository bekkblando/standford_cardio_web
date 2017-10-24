import React, { Component } from 'react';
import logo from './logo.svg';
import TinyMCE from 'react-tinymce';
import './App.css';

class App extends Component {
  handleEditorChange(e) {
    console.log(e.target.getContent());
  }
  render() {
    return (
      <TinyMCE
        content="<p>This is the initial content of the editor</p>"
        config={{
          plugins: 'autolink link image lists print preview',
          toolbar: 'undo redo | bold italic | alignleft aligncenter alignright'
        }}
        onChange={this.handleEditorChange}
      />
    );
  }
}

export default App;
