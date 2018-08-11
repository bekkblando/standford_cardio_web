import React, { Component } from 'react';


class NavBar extends Component {
  render () {
      if(window.location.pathname != '/viewContent'){
        return(
          <nav className = "navbar navbar-expand-lg">
            <div className = "navbar-nav">
              <ul className = "navbar-nav">
                <li className='navbar-brand right'>
                  <img src="stanford_medicine_logo.png" width="200" alt=""/>
                </li>
                { this.props.auth &&
                    <li className='nav-item'><a className = 'nav-link' href = "/manual">Manual</a></li>
                }
                { this.props.auth &&
                    <li className='nav-item'><a className = 'nav-link' href = "/versions">Versions</a></li>
                }
                { this.props.auth &&
                  <li className='nav-item'><a className = 'nav-link' href = "/logout">Logout</a></li>
                }
                { !this.props.auth &&
                  <li className='nav-item'><a href = "/login">Login</a></li>
                }
              </ul>
            </div>
          </nav>
      );
    }else{
      return(<span></span>)
    }
  }
}

export default NavBar;
