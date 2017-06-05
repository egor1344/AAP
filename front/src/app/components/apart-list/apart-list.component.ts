import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { Apartment }        from '../../apartment';
import { ApartmentService } from '../../service/apartment.service';

@Component({
  selector: 'app-apart-list',
  templateUrl: './apart-list.component.html',
  styleUrls: ['./apart-list.component.css']
})

export class ApartListComponent implements OnInit {

  apartments: Apartment[];

  constructor(
    private apartmentService: ApartmentService,
    private router: Router
  ) { }

  getApartments() {
    this.apartmentService.getApartments()
               .subscribe(apart => {this.apartments = apart;});

  }

  ngOnInit():void {
    this.getApartments();
    // console.log(this.apartments);
  }

  onClick(id){
    this.router.navigate(['/detail/', id])
  }

}
