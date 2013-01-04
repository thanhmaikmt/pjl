//
//  Piece.m
//  Trainyard
//
//  Created by Matt Rix on 09-10-03.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import "Piece.h"
#import "Cell.h"
#import "PieceDecoder.h"

@implementation Piece

@synthesize pieceType = _pieceType;
@synthesize cell = _cell;



+(id) pieceWithPieceType: (PieceType) pieceType andCell: (Cell*) cell
{
	return [[[Piece alloc] initWithPieceType:pieceType andCell:cell] autorelease];
}

-(id) initWithPieceType: (PieceType) pieceType andCell: (Cell*) cell
{
	self = [super init];
	if(self)
	{
		_pieceType = pieceType;
		_cell = cell;
	}
	return self;
}

-(void) toEncodedChars: (char[]) chars
{
	chars = "";
}

+(PieceDecoder*) pieceDecoderFromEncodedChars: (char[]) chars
{
	return nil;
}

-(BOOL)isEqualToPiece:(Piece*)otherPiece
{
    return ([[self description] isEqualToString:[otherPiece description]]); //a little crude, but it works
}

-(NSString*) description
{
	return [NSString stringWithFormat:@"{Piece %@}", NSStringFromPieceType(_pieceType)];
}

-(void) dealloc
{
	//NSLog(@"deallocing a piece");
	[super dealloc];
}

@end

extern NSString *NSStringFromPieceType(PieceType pieceType)
{
	switch(pieceType)
	{
		case PieceType_Empty:		return @"Empty";
		case PieceType_Rock:		return @"Rock";
		case PieceType_Track:		return @"Track";
		case PieceType_Outlet:		return @"Outlet";	
		case PieceType_Goal:		return @"Goal";
		case PieceType_Splitter:	return @"Splitter";
		case PieceType_Painter:		return @"Painter";
	}
	
	return @"PieceTypeNotValid";
}



