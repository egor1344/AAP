import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ActivatedRoute, Params } from '@angular/router';
import { Location }               from '@angular/common';

import 'rxjs/add/operator/switchMap';

import { Apartment }        from '../../apartment';
import { ApartmentService } from '../../service/apartment.service';

@Component({
  selector: 'app-apart-list',
  templateUrl: './apart-list.component.html',
  styleUrls: ['./apart-list.component.css']
})

export class ApartListComponent implements OnInit {

  apartments: Apartment[];
  num: number;
  next: String;
  isPrevious: String;
  previous: String;


  constructor(
    private apartmentService: ApartmentService,
    private router: Router,
    private route: ActivatedRoute,
    private location: Location
  ) { }

  getApartments() {

    this.route.params
       .switchMap((params: Params) => {
         this.num = +params['num'];
         return this.apartmentService.getApartments(this.num);
       }).subscribe(take_apartment => {
         console.log(take_apartment);
         this.apartments = take_apartment.results;
         this.next = '/apartments/' + (this.num + 1);
         this.isPrevious = take_apartment.previous;
         if (this.isPrevious != 'null'){
           this.previous = '/apartments/' + (this.num - 1);
         }
       });

  }

  ngOnInit():void {
    this.getApartments();
    // console.log(this.apartments);
  }

  onClick(id){
    this.router.navigate(['/detail/', id])
  }

}
