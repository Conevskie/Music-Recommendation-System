import { Component, OnInit } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {MusicServiceService} from "../music-service.service";

@Component({
  selector: 'app-music-cards',
  templateUrl: './music-cards.component.html',
  styleUrls: ['./music-cards.component.scss']
})
export class MusicCardsComponent implements OnInit {

  recommendedTracks: any[] = [];
  allTracks: any[] = [];
  chosenTrackId: string;

  constructor(private http: HttpClient, private musicService: MusicServiceService) { }

  ngOnInit(): void {
    this.musicService.chosenSong.subscribe(song => {
      this.chosenTrackId = song[1];
      this.getAllRecommendations(this.chosenTrackId)
      console.log(this.recommendedTracks)
      this.recommendedTracks = [];
    });

    this.musicService.getTrackData().subscribe((tracks: any) => {
      this.allTracks = tracks;
    });
  }

  getAllRecommendations(chosenTrackId: any): void {
    let recommendations: any = {};

    this.allTracks.forEach((track: any) => {
      if (track['id'] == chosenTrackId) {

        recommendations = {
          'recommendations': track['recommendations'],
          'similarity_score': track['similarity_scores']
        }
        console.log(recommendations)
        recommendations['recommendations'].forEach((track_id: string, index: number) => {
          this.musicService.getTrack(track_id).subscribe((data: any) => {
            if (data) {
              data['similarity_score'] = recommendations['similarity_score'][index]
              this.recommendedTracks.push(data);
            }
          });
        })
      }
    });
  }

  openUrl(url: string) {
    window.open(url, "_blank");
  }

}
