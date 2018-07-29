import React, { Component } from 'react';

import {
    AccordionItem,
    AccordionItemTitle,
    AccordionItemBody
} from 'react-accessible-accordion';

class ManualSection extends Component {

  constructor(props){
    super(props);
    this.state = {
      loading: true,
      sections: ''
    };
  }

  componentWillMount() {
    // Get the Manual Section
    this.setState({loading: true});
    let sections = []
    this.props.manual_ref.once("value", (section, index) => {
      sections.push([<AccordionItem key={section.key}><span>{section.key}</span></AccordionItem>]);
    }).then(() => {
      this.setState({sections: sections, loading: false});
    });
  }

  render() {

    if(this.state.loading){
      return(
        <AccordionItemBody>
          <AccordionItemTitle>
            Loading
          </AccordionItemTitle>
        </AccordionItemBody>
      )
    }

    // Display a Table of Contents with view and edit buttons the second
    // and third level sections
    return (
        <AccordionItemBody>
          {
            !this.state.loading && this.state.sections
          }
        </AccordionItemBody>
    );
  }
}

export default ManualSection;
