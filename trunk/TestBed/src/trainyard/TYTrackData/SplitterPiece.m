//
//  SplitterPiece.m
//  Trainyard
//
//  Created by Matt Rix on 09-10-03.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import "SplitterPiece.h"
#import "Cell.h"
#import "TYColor.h"
#import "TYSide.h"
#import "PieceDecoder.h"
#import "YardStringEncoder.h"
#import "Train.h"

@implementation SplitterPiece

@synthesize sideIn = _sideIn;

- (id)initWithSideIn:(TYSide*)sideIn andCell:(Cell*)cell;
{
	self = [super initWithPieceType:PieceType_Splitter andCell:cell];
	if(self)
	{
		_sideIn = sideIn;
		_trainsToCreate = [[NSMutableArray alloc] init];	
		[self updateSidesOut];
	}
	return self;
}

-(void) updateSidesOut
{
	_sideOutLeft = [TYSide sideFromValue:(_sideIn.value+1)%4];
	_sideOutRight = [TYSide sideFromValue:(_sideIn.value+3)%4];
	
}

-(void) fireMajorChange
{
	[self updateSidesOut];
	[super fireMajorChange];
}

-(BOOL) hasTrains
{
	return ([_trainsToCreate count] > 0);
}

-(NSArray*) getTrainsToCreate
{
	NSArray *result = [NSArray arrayWithArray:_trainsToCreate];
	
	[_trainsToCreate removeAllObjects];
	
	return result;
}


-(BOOL) giveEdgeTrain:(Train*)train fromIncomingSide:(TYSide*)incomingSide
{
	if(_sideIn == incomingSide)
	{
		train.nextSide = incomingSide.opposite;
		return YES;
	}
	else
	{
		return NO;
	}
}

-(BOOL) giveCenterTrain:(Train*)train fromIncomingSide:(TYSide*)incomingSide
{
	TYColor *trainColor = train.color;
	TYColor *leftColor;
	TYColor *rightColor;
	
	if([trainColor.primaries count] >= 2)
	{
		leftColor = [trainColor.primaries objectAtIndex:0];
		rightColor = [trainColor.primaries objectAtIndex:1];		
	}
	else
	{
		leftColor = trainColor;
		rightColor = trainColor; 
	}
	
	[_trainsToCreate addObject:[[[Train alloc] initWithColor:leftColor 
													andPiece:self 
												 andNextSide:_sideOutLeft] autorelease]];
	
	[_trainsToCreate addObject:[[[Train alloc] initWithColor:rightColor 
													andPiece:self 
												 andNextSide:_sideOutRight] autorelease]];	
	
	[train kill];
	
	if([_delegate respondsToSelector:@selector(onSplit)])
	{
		[(id)_delegate onSplit];
	}
	
	if([_viewDelegate respondsToSelector:@selector(onSplit)])
	{
		[(id)_viewDelegate onSplit];
	}
	
	return YES;
}


-(void) toEncodedChars: (char[]) chars
{
	chars[0] = 'S';
	chars[1] = charFromInt(_sideIn.value);
	chars[2] = '\0';
}

+(PieceDecoder*) pieceDecoderFromEncodedChars: (char[]) chars
{
	TYSide *sideIn = [TYSide sideFromValue:intFromChar(chars[1])];

	SplitterPiece *piece = [[[SplitterPiece alloc] initWithSideIn:sideIn andCell:nil] autorelease];
	return [PieceDecoder pieceDecoderWithPiece:piece andNumCharsToRemove:2];
}

- (id)copyWithZone:(NSZone *)zone
{
	return  [[[self class] alloc] initWithSideIn:_sideIn andCell:_cell];
}

-(NSString*) description
{
	return [NSString stringWithFormat:@"{Piece %@ SideIn:%@}", NSStringFromPieceType(_pieceType), _sideIn];
}

-(void) dealloc
{
	[_trainsToCreate release];
	[super dealloc];
}


@end
