import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ApartListComponent } from './apart-list.component';

describe('ApartListComponent', () => {
  let component: ApartListComponent;
  let fixture: ComponentFixture<ApartListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ApartListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ApartListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
