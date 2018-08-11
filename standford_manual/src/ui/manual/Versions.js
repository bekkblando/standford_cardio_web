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
      loading: true,
      diffs: '',
    };
  }

  renderChange(changeHash){
    return(
      Object.entries(changeHash).map((entrie) => {
        return(<div className="accordion">
          <div className='card'>
            <div className="card-header">
              <a data-toggle="collapse" href={'#' + entrie[0]} role="button" aria-expanded="true">
                { entrie[0] }
              </a>
            </div>
            <div id = { entrie[0] } className="collapse">
              {
                entrie[0] != "content" ?
                  this.renderChange(entrie[1])
              :
                <div>
                  Content Change
                </div>
              }
            </div>
          </div>
        </div>)
      })
    )
  }

  createDiffs(diffHash){
    let diff_type;
    let value;
    let components = [];
    Object.entries(diffHash).map((entrie) => {
      console.log("This is real")
      diff_type = entrie[0];
      value = entrie[1];
      if(diff_type.includes('deletion')){
        console.log("Delation")
        components.push(
          <div>
            <button onClick={(e) => this.undo(diff_type) }>Undo</button>
            <div>
              Deleted
            </div>
            { value.replace("/", " ").split(" ").map((section) => <span>{section} ></span>) }
          </div>)
      }else if(diff_type.includes('change')){
        components.push(<div><button onClick={(e) => this.undo(diff_type) }>Undo</button>{ this.renderChange(value) }</div>);
      }
    });
    console.log("components", components)
    this.setState({diffs: components, loading: false})
  }

  componentWillMount() {
    // Get the manual
    let manual_ref = firebase.database().ref().child('versions');
    manual_ref.once("value", (section, index) =>{
    }).then((value) => {
      this.createDiffs(value.val())
    });
  }

  render() {

    if(this.state.loading){
      return(<div>Loading</div>)
    }

    // Display a Table of Contents with view and edit buttons the second
    // and third level sections
    console.log("Diffs", this.state.diffs)
    return (
      <span>
        {
          !this.state.loading && <span>{this.state.diffs}</span>
        }
      </span>
    );
  }
}

export default Manual;
