import firebase from '../../init_firebase';
import React, { Component } from 'react';
import Content from './Content';
import EditContent from './EditContent';
import NavBar from '../NavBar';
import { Link } from "react-router-dom";

import {
    Accordion,
    AccordionItem,
    AccordionItemTitle,
    AccordionItemBody,
} from 'react-accessible-accordion';

class Manual extends Component {

  constructor(props){
    super(props);
    this.state = {
      loading: false,
      sections: '',
      version: 0
    };
  }

  deleteSection(location){
    if (window.confirm("Are you sure you would like to delete this section?")) {
      let deletion_data = {};
      deletion_data['/versions/deletion_' + this.state.version] = location;
      firebase.database().ref().update(deletion_data);
      firebase.database().ref().update({'/versions/version': this.state.version + 1});
      firebase.database().ref().child(location).remove();
    }
  }

  componentWillMount() {
    // Get the manual
    let manual_ref = firebase.database().ref().child(this.props.passedProps.manual_location);
    let manual;
    manual_ref.once("value", (section, index) =>{
      if(section != "content"){
        manual = section.val()
      }
    }).then((value) => {
      let sections = []
      let component;
      Object.keys(manual).map((section) =>{
            component =
                <div className="accordion">
                  <div className='card'>
                    <div className="card-header">
                      <a data-toggle="collapse" href={'#'+this.props.passedProps.manual_location + "/" + section + "/"} role="button" aria-expanded="true" aria-controls={this.props.passedProps.manual_location}>
                        {section}
                      </a>
                    </div>
                    <div id = {this.props.passedProps.manual_location + "/" + section + "/"} className="collapse">
                      {
                        section != "content" ?
                        <div className = "card-body">
                          <Manual passedProps={{manual_location: this.props.passedProps.manual_location + "/" + section + "/"}}/>
                        </div>
                      :
                        <span>
                          <Link to={ "/editContent?" + this.props.passedProps.manual_location }> Edit Content </Link>
                          <Link to={ "/viewContent?" + this.props.passedProps.manual_location }> View Content </Link>
                          <button onClick = { (e) => this.deleteSection(this.props.passedProps.manual_location) }>Delete Section</button>
                        </span>
                      }
                    </div>
                  </div>
                </div>
            sections.push(component);
        });
        firebase.database().ref().child("/versions/version").once("value", (section, index) =>{
        }).then((value) => {
          this.setState({version: value.val()});
        });
        this.setState({sections: sections, loading: true});
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
          this.state.loading && <span>{this.state.sections}</span>
        }
      </span>
    );
  }
}

export default Manual;
