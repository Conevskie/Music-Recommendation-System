import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MusicCardsComponent } from './music-cards.component';

describe('MusicCardsComponent', () => {
  let component: MusicCardsComponent;
  let fixture: ComponentFixture<MusicCardsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MusicCardsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MusicCardsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
