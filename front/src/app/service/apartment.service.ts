import { Injectable } from '@angular/core';
import { Headers, Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { Apartment } from '../apartment';

@Injectable()
export class ApartmentService {

  private headers = new Headers({'Content-Type': 'application/json'});
  private apartmentsUrl = 'api/v1.0/'; // Url
  private authUrl = 'api-auth/';
  private hostUrl = 'http://localhost:8000/'

  constructor(private http: Http) { }

  getApartments() {
    this.authClient();
    return this.http.get(this.hostUrl + this.apartmentsUrl)
               .toPromise()
               .then(response => response.json().data as Apartment[])
               .catch(this.handleError);
  }

  private handleError(error: any): Promise<any>{
    console.error("Ошибка при получении списка квартир");
    return Promise.reject(error.message || error);
  }

  private authClient() {
    let rec = {
      username: 'marko',
      password: 'qwertyasdfg'
    };
    this.http.post(this.hostUrl + this.authUrl, JSON.stringify(rec), {headers: this.headers})
               .toPromise()
               .then(() => console.log('Auth success'))
               .catch(this.handleError);
  }

}
