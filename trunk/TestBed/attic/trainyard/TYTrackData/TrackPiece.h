//
//  TrackPiece.h
//  Trainyard
//
//  Created by Matt Rix on 09-10-03.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "Piece.h"
#import "DestinationPieceProtocol.h"

@class TYSide;
@class TYTrack;

@interface TrackPiece : Piece <DestinationPieceProtocol>
{
	TYTrack *_primaryTrack;
	TYTrack *_secondaryTrack;
	BOOL _isSwitchable;
}

@property (nonatomic, readwrite, assign) TYTrack *primaryTrack;
@property (nonatomic, readwrite, assign) TYTrack *secondaryTrack;
@property (nonatomic, readonly) BOOL isSwitchable;

-(id)initWithPrimaryTrack: (TYTrack*)primaryTrack andSecondaryTrack:(TYTrack*)secondaryTrack andCell:(Cell*)cell;
-(void) switchTracks;
-(void) updateSwitchable;

-(void)erase;
-(void)undo;

-(TYTrack*) trackForSide: (TYSide*)side;

+(TrackPiece*) trackPieceFromChar: (char) trackChar;


@end

@protocol TrackPieceDelegate <NSObject>

-(void)onErase;
-(void)onUndo;

@end

