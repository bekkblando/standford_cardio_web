// This component handles the App template used on every page.
import React from 'react';
import PropTypes from 'prop-types';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { connect } from 'react-redux';
import Manual from './ui/manual/Manual';
import Content from './ui/manual/Content';
import Login from './auth/Login';
import NavBar from './ui/NavBar';
import LogoutButton from './auth/LogoutButton';
import PrivateRoute from './auth/PrivateRoute';

const App = ({ authenticated, checked }) => (
  <div>
    <Router>
      { checked &&
        <div>
          <PrivateRoute exact path = "/manual" component={Manual} passedProp={{props: {manual_location: "0/Manual"}}} authenticated={authenticated}/>
          <Route path = '/viewContent' component = { Content }  authenticated={authenticated}/>
          <Route path = "/logout" component = { LogoutButton } />
          <Route path = "/login" component = { Login } />
        </div>
      }
    </Router>
  </div>
);

const { bool } = PropTypes;

App.propTypes = {
  authenticated: bool.isRequired,
  checked: bool.isRequired
};

const mapState = ({ session }) => ({
  checked: session.checked,
  authenticated: session.authenticated
});

export default connect(mapState)(App);
