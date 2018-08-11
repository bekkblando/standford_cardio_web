import React, { Component } from 'react';
import firebase from '../../init_firebase';

class EditContent extends Component {

  constructor(props){
    super(props);
    this.state = {
      loading: false,
      content: '',
      version: 0
    };
  }

  updateState(){
    this.manual_ref = firebase.database().ref().child(decodeURIComponent(this.props.location.search).substr(1));
    this.manual_ref.once("value", (section, index) =>{
    }).then((value) => {
      this.setState({content: value.val().content, loading: true});
    });
    firebase.database().ref().child("/versions/version").once("value", (section, index) =>{
    }).then((value) => {
      console.log(value.val())
      this.setState({version: value.val()});
    });
  }

  componentWillMount() {
    this.updateState();
  }

  componentDidUpdate(){
    window.tinymce.init({
      selector: '.editContent',
     menubar: false,
     height: 500,
     plugins: [
       'advlist autolink lists link image charmap print preview anchor textcolor',
       'searchreplace visualblocks code fullscreen',
       'insertdatetime media table contextmenu paste code help wordcount'
     ],
     toolbar: 'insert | undo redo |  formatselect | bold italic backcolor  | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | help',
     content_css: ['/css/style.css']
    });
  }

  saveSection(){
    let update_data = {}
    update_data[decodeURIComponent(this.props.location.search).substr(1).replace("0/", "versions/").replace("Manual", "change_" + this.state.version)+'content'] = window.tinyMCE.get('editiableContent').getContent({format : 'raw'});
    firebase.database().ref().update(update_data);
    firebase.database().ref().update({'/versions/version': this.state.version + 1});
    this.manual_ref.set({'content': window.tinyMCE.get('editiableContent').getContent({format : 'raw'})}).then(() => alert('Saved'));
    this.updateState();
  }

  render() {

    if(!this.state.loading){
      return(<div>Loading</div>)
    }

    // Display a Table of Contents with view and edit buttons the second
    // and third level sections
    return (
      <div>
          <div className='container'>
            <button type="button" onClick = {() => this.saveSection() } className="btn btn-dark">Save</button>
            {
              this.state.loading && <textarea className = "editContent" id = "editiableContent">{this.state.content}</textarea>
            }
          </div>
      </div>
    );

  }
}

export default EditContent;
