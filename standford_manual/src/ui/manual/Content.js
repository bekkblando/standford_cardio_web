import React, { Component } from 'react';
import firebase from '../../init_firebase';

class Content extends Component {

  constructor(props){
    super(props);
    this.state = {
      loading: false,
      content: ''
    };
  }

  componentWillMount() {
    let manual_ref = firebase.database().ref().child(decodeURIComponent(this.props.location.search).substr(1));
    manual_ref.once("value", (section, index) =>{
    }).then((value) => {
      this.setState({content: value.val().content, loading: true});
    });
  }

  render() {

    if(!this.state.loading){
      return(<div>Loading</div>)
    }

    // Display a Table of Contents with view and edit buttons the second
    // and third level sections
    return (
      <span>
        {
          this.state.loading && <div dangerouslySetInnerHTML = { { __html: this.state.content } }></div>
        }
      </span>
    );

  }
}

export default Content;
