import {AfterViewInit, Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {MusicServiceService} from "../music-service.service";
import {fromEvent} from "rxjs";
import {debounceTime, distinctUntilChanged, tap} from "rxjs/operators";

@Component({
  selector: 'app-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.scss']
})
export class SearchBarComponent implements OnInit, AfterViewInit {

  @ViewChild('input') input: ElementRef;
  searchedTracks: any = [];
  isRecommendations: boolean = false;

  constructor(private musicService: MusicServiceService) {}

  ngOnInit(): void {
    this.musicService.filteredTracks.subscribe(t => {
      const numberOfTracks = 3;
      this.searchedTracks = t.slice(0, numberOfTracks);
      this.isRecommendations = t.length !== 0;
    });
  }

  ngAfterViewInit(): void {
    this.search();
  }

  search(): void {
    fromEvent(this.input.nativeElement, 'keyup')
      .pipe(
        debounceTime(500),
        distinctUntilChanged(),
        tap(() => {
          this.musicService.filterInput(this.input.nativeElement.value);
        })
      ).subscribe()
  }

  recommendForTrack(track: any) {
    this.musicService.chosenSong.next(track);
  }
}
