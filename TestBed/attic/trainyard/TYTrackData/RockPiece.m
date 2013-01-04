//
//  RockPiece.m
//  Trainyard
//
//  Created by Matt Rix on 09-10-03.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import "RockPiece.h"
#import "Cell.h"
#import "PieceDecoder.h"

@implementation RockPiece

- (id)initWithCell: (Cell*) cell
{
	self = [super initWithPieceType:PieceType_Rock andCell:cell];
	return self;
}

-(void) toEncodedChars: (char[]) chars
{
	chars[0] = 'R';
    chars[1] = '\0';
}

+(PieceDecoder*) pieceDecoderFromEncodedChars: (char[]) chars
{
	RockPiece *piece = [[[RockPiece alloc] initWithCell:nil] autorelease];
	return [PieceDecoder pieceDecoderWithPiece:piece andNumCharsToRemove:1];
}

- (id)copyWithZone:(NSZone *)zone
{
	return  [[[self class] alloc] initWithCell:_cell];
}


@end
