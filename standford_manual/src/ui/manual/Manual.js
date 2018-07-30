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
      sections: ''
    };
  }

  saveSection(section){

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
                        </span>
                      }
                    </div>
                  </div>
                </div>
            sections.push(component);
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
