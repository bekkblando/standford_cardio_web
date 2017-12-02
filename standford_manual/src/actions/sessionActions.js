import { sessionService } from 'redux-react-session';
import * as sessionApi from '../api/sessionApi.js';

export const login = (user, history) => {
  return () => {
    return sessionApi.login(user).then(response => {
      // Invalid user
      if(response["token"] === 0){
        throw response["email"];
      }
      const { token } = response;
      sessionService.saveSession({ token })
      .then(() => {
        sessionService.saveUser(response.data)
        .then(() => {
          history.push('/');
        }).catch(err => console.error(err));
      }).catch(err => console.error(err));
    });
  };
};

export const logout = (history) => {
  return () => {
    return sessionApi.logout().then(() => {
      sessionService.deleteSession();
      sessionService.deleteUser();
      history.push('/login');
    }).catch(err => {
      throw (err);
    });
  };
};
