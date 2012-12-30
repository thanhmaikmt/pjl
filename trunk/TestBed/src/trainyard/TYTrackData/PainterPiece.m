//
//  PainterPiece.m
//  Trainyard
//
//  Created by Matt Rix on 09-10-03.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import "PainterPiece.h"
#import "Cell.h"
#import "TYColor.h"
#import "TYSide.h"
#import "TYTrack.h"
#import "PieceDecoder.h"
#import "YardStringEncoder.h"
#import "Train.h"

@implementation PainterPiece

@synthesize color = _color;
@synthesize sideA = _sideA;
@synthesize sideB = _sideB;

- (id)initWithColor:(TYColor*)color andSideA:(TYSide*)sideA andSideB:(TYSide*)sideB andCell:(Cell*)cell
{
	self = [super initWithPieceType:PieceType_Painter andCell:cell];
	if(self)
	{
		_color = color; 
		
		_sideA = sideA;
		_sideB = sideB;
	}
	return self;
}

-(BOOL) giveEdgeTrain:(Train*)train fromIncomingSide:(TYSide*)incomingSide
{
	if(incomingSide == _sideA)
	{
		train.nextSide = _sideB;
		train.currentTrack = [TYTrack trackFromSideA:incomingSide andSideB:_sideB];
		return YES;
	}
	else if(incomingSide == _sideB)
	{
		train.nextSide = _sideA;
		train.currentTrack = [TYTrack trackFromSideA:incomingSide andSideB:_sideA];
		return YES;
	}
	else
	{
		return NO;
	}
}

-(BOOL) giveCenterTrain:(Train*)train fromIncomingSide:(TYSide*)incomingSide
{
	train.color = _color;
	
	if([_delegate respondsToSelector:@selector(onPaint)])
	{
		[(id)_delegate onPaint];
	}
	
	if([_viewDelegate respondsToSelector:@selector(onPaint)])
	{
		[(id)_viewDelegate onPaint];
	}
	
	return YES;
}

-(void) toEncodedChars: (char[]) chars
{
	chars[0] = 'P';
	chars[1] = charFromInt(_color.value);
	chars[2] = charFromInt(_sideA.value*7+_sideB.value);
	chars[3] = '\0';
}

+(PieceDecoder*) pieceDecoderFromEncodedChars: (char[]) chars
{
	int colorValue = intFromChar(chars[1]);
	int sidesValue = intFromChar(chars[2]);

	TYColor *color = [TYColor colorFromValue:colorValue];
	
	TYSide *sideA = [TYSide sideFromValue:floorf((float)sidesValue/7)];
	TYSide *sideB = [TYSide sideFromValue:sidesValue%7];
	
	PainterPiece *piece = [[[PainterPiece alloc] initWithColor:color andSideA: sideA andSideB:sideB andCell:nil] autorelease];
	return [PieceDecoder pieceDecoderWithPiece:piece andNumCharsToRemove:3];
}

- (id)copyWithZone:(NSZone *)zone
{
	return  [[[self class] alloc] initWithColor:_color andSideA:_sideA andSideB:_sideB andCell:_cell];
}

-(NSString*) description
{
	return [NSString stringWithFormat:@"{Piece %@ Color:%@ Sides:%@,%@ }", NSStringFromPieceType(_pieceType), _color, _sideA, _sideB];
}

-(void) dealloc
{
	[super dealloc];
}


@end
