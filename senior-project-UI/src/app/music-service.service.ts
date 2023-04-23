import {EventEmitter, Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import data from '../assets/json_full_data.json';
import {BehaviorSubject} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class MusicServiceService {

  //token needs to be generated every hour because of the use of the developer Spotify API
  accessToken: string = 'BQC-Q7vQTeyA1-PiiC-jHrpR6OifqHBsq8usFtWmipsHbJaMj8_b81nlAZRB3qOa7BXNrV_y2wQgXQI-EyZDw8Dsjzy8bcegQSCLtQWhzQH0hLBWWiE';
  endpoint: string = 'https://api.spotify.com/v1/tracks/';
  jsonPath: string = '../assets/json_full_data.json';
  filteredTracks = new BehaviorSubject<any[]>([]);
  chosenSong: EventEmitter<string> = new EventEmitter<string>();

  private httpOptions = {
    headers: new HttpHeaders({
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.accessToken
    })
  }

  constructor(private http: HttpClient) { }

  getTrack(trackId: string): any {
    return this.http.get(this.endpoint + trackId,  this.httpOptions)
  }

  getTrackData(): any{
    return this.http.get(this.jsonPath);
  }

  filterInput(filter: string) {
    let filteredTracks: any[] = [];

    if (filter) {
      // @ts-ignore
      data.forEach(track => {
        if (track.name.toLowerCase().includes(filter.toLowerCase())) {
          filteredTracks.push([track.name, track.id]);
        }
      });
    }
    this.filteredTracks.next(filteredTracks);
  }

}
