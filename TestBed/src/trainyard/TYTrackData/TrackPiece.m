//
//  TrackPiece.m
//  Trainyard
//
//  Created by Matt Rix on 09-10-03.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import "TrackPiece.h"
#import "Cell.h"
#import "TYSide.h"
#import "TYTrack.h"
#import "PieceDecoder.h"
#import "YardStringEncoder.h"
#import "Train.h"
#import "TYSoundManager.h"

@implementation TrackPiece

@synthesize primaryTrack = _primaryTrack;
@synthesize secondaryTrack = _secondaryTrack;
@synthesize isSwitchable = _isSwitchable;

-(id)initWithPrimaryTrack: (TYTrack*)primaryTrack andSecondaryTrack:(TYTrack*)secondaryTrack andCell:(Cell*)cell;
{
	self = [super initWithPieceType:PieceType_Track andCell:cell];
	if(self)
	{
		_primaryTrack = primaryTrack;
		_secondaryTrack = secondaryTrack;
		
		if(!_primaryTrack) _primaryTrack = [TYTrack trackFromValue:TYTrack_Empty];
		if(!_secondaryTrack) _secondaryTrack = [TYTrack trackFromValue:TYTrack_Empty];
		
		[self updateSwitchable];
	}
	return self;
}

-(void) erase
{
	if([_delegate respondsToSelector:@selector(onErase)])
	{
		[(id)_delegate onErase];
	}
	if([_viewDelegate respondsToSelector:@selector(onErase)])
	{
		[(id)_viewDelegate onErase];
	}   
}

-(void) undo
{
	if([_delegate respondsToSelector:@selector(onUndo)])
	{
		[(id)_delegate onUndo];
	}
	if([_viewDelegate respondsToSelector:@selector(onUndo)])
	{
		[(id)_viewDelegate onUndo];
	}  
}

-(BOOL) giveEdgeTrain:(Train*)train fromIncomingSide:(TYSide*)incomingSide
{
	TYTrack *track = [self trackForSide:incomingSide];
	
	if(track)
	{
		train.nextSide = [track getOtherSide:incomingSide];
		train.currentTrack = track;;
		return YES;
	}
	else
	{
		return NO;
	}
}

-(BOOL) giveCenterTrain:(Train*)train fromIncomingSide:(TYSide*)incomingSide
{
	return YES;
}



-(void) switchTracks
{
	if(_isSwitchable && _secondaryTrack.value != TYTrack_Empty)
	{
		TYTrack *oldPrimaryTrack = _primaryTrack;
		_primaryTrack = _secondaryTrack;
		_secondaryTrack = oldPrimaryTrack;
		
		[TheSoundManager playSound:@"Game_SwitchTrack"];
		
		[self fireMajorChange];
	}
}

-(void) fireMajorChangeWithThingThatChanged:(id)thingThatChanged
{
	[self updateSwitchable];
	[super fireMajorChangeWithThingThatChanged:thingThatChanged];
}

-(void) updateSwitchable
{
	//if the two tracks have ANY sides in common, it's switchable
	_isSwitchable = (BOOL)(_secondaryTrack.value != TYTrack_Empty &&   
					((_primaryTrack.sideA == _secondaryTrack.sideA) || 
					 (_primaryTrack.sideA == _secondaryTrack.sideB) ||
					 (_primaryTrack.sideB == _secondaryTrack.sideA) || 
					 (_primaryTrack.sideB == _secondaryTrack.sideB) 
					 ));
}

-(TYTrack*) trackForSide: (TYSide*)side
{
	if([_primaryTrack hasSide:side])
	{
		return _primaryTrack;
	}
	else if([_secondaryTrack hasSide:side])
	{
		return _secondaryTrack;
	}
	
	return nil;
}


-(void) toEncodedChars: (char[]) chars
{
	chars[0] = charFromInt(_secondaryTrack.value + _primaryTrack.value*7);
	chars[1] = '\0';
}



+(TrackPiece*) trackPieceFromChar: (char) trackChar
{
	int charValue = intFromChar(trackChar);
	TYTrack *primaryTrack = [TYTrack trackFromValue:floorf((float)charValue/7)];
	TYTrack *secondaryTrack = [TYTrack trackFromValue:charValue%7];
	return [[[TrackPiece alloc] initWithPrimaryTrack:primaryTrack andSecondaryTrack:secondaryTrack andCell:nil] autorelease];
}

- (id)copyWithZone:(NSZone *)zone
{
	return  [[[self class] alloc] initWithPrimaryTrack:_primaryTrack andSecondaryTrack:_secondaryTrack andCell:_cell];
}

-(NSString*) description
{
	return [NSString stringWithFormat:@"{Piece %@ Primary:%@ Secondary:%@}", NSStringFromPieceType(_pieceType), _primaryTrack, _secondaryTrack];
}

-(void) dealloc
{
	[super dealloc];
}


@end
