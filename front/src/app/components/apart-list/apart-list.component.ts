import { Component, OnInit } from '@angular/core';
import { Router }            from '@angular/router';

import { Apartment }        from '../../apartment';
import { ApartmentService } from '../../service/apartment.service'
import {AuthService }       from '../../service/auth.service';

@Component({
  selector: 'app-apart-list',
  templateUrl: './apart-list.component.html',
  styleUrls: ['./apart-list.component.css']
})
export class ApartListComponent implements OnInit {

  private apartments: Apartment[];

  constructor(
    private router: Router,
    private apartmentService: ApartmentService,
    private authService: AuthService
  ) { }

  getApartments() {
    this.apartmentService.getApartments(this.authService.getToken())
               .subscribe(apart => {
                 console.log(apart);
                 this.apartments = apart;
               });

  }

  ngOnInit():void {
    this.getApartments();
    console.log(this.apartments);
  }

}
