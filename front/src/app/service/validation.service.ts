import { Injectable } from '@angular/core';

@Injectable()
export class ValidationService {

  constructor() { }

  validateLogin(login){
    if(login.length < 4){
      return true;
    } else {
      return false;
    }
  }

  validateEmail(email) {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
  }

  validatePass(pass1, pass2){
    if (pass1 === pass2){
      return true;
    } else {
      return false;
    }
  }

}
