import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import registerServiceWorker from './registerServiceWorker';
import './index.css';
import { Provider } from 'react-redux';
import thunkMiddleware from 'redux-thunk';
import { combineReducers, createStore, compose, applyMiddleware } from 'redux';
import { sessionService, sessionReducer } from 'redux-react-session';

const reducers = {
  session: sessionReducer
};
const reducer = combineReducers(reducers);

const store = createStore(reducer, undefined, compose(applyMiddleware(thunkMiddleware)));

sessionService.initSessionService(store);


ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>, document.getElementById('app')
);

registerServiceWorker();
