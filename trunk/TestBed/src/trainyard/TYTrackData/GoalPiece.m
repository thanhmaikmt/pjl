//
//  GoalPiece.m
//  Trainyard
//
//  Created by Matt Rix on 09-10-03.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import "GoalPiece.h"
#import "Cell.h"
#import "TYColor.h"
#import "TYSide.h"
#import "PieceDecoder.h"
#import "YardStringEncoder.h"
#import "Train.h"
#import "TYTrack.h"
#import "TYSoundManager.h"

@implementation GoalPiece

@synthesize colors = _colors;
@synthesize sidesIn = _sidesIn;

- (id)initWithColors:(NSMutableArray*)colors andSidesIn:(NSMutableArray*)sidesIn andCell:(Cell*)cell;
{
	self = [super initWithPieceType:PieceType_Goal andCell:cell];
	if(self)
	{
		_colors = [colors retain]; 
		_sidesIn = [sidesIn retain];
	}
	return self;
}

-(BOOL) giveEdgeTrain:(Train*)train fromIncomingSide:(TYSide*)incomingSide
{
	if([_sidesIn indexOfObject:incomingSide] != NSNotFound)
	{
		train.nextSide = incomingSide.opposite;
		train.currentTrack = [TYTrack trackFromSideA:incomingSide andSideB:incomingSide.opposite];
		return YES;
	}
	else
	{
		return NO;
	}
}

-(BOOL) giveCenterTrain:(Train*)train fromIncomingSide:(TYSide*)incomingSide
{
	int colorIndex = [_colors indexOfObject:train.color];
	if(colorIndex != NSNotFound)
	{
		
		[TheSoundManager playTrainSoundForIndex:train.color.value];
		
		[_colors removeObjectAtIndex:colorIndex];
		[train kill];
		
		if([_delegate respondsToSelector:@selector(onGetTrain:)])
		{
			[(id)_delegate onGetTrain:colorIndex];
		}
		
		if([_viewDelegate respondsToSelector:@selector(onGetTrain:)])
		{
			[(id)_viewDelegate onGetTrain:colorIndex];
		}
		
		[self fireMinorChange]; //a major change would have made the view create all new nubs
		
		return YES;
	}
	else
	{
		[train kill];
		return NO;
	}
}


-(BOOL) isEmpty
{
	return ([_colors count] == 0);
}

-(void) toEncodedChars: (char[]) chars
{
	
	int sideValue = 
	[_sidesIn containsObject:[TYSide sideFromShortForm:'t']] * 1 + 
	[_sidesIn containsObject:[TYSide sideFromShortForm:'r']] * 2 + 
	[_sidesIn containsObject:[TYSide sideFromShortForm:'b']] * 4 + 
	[_sidesIn containsObject:[TYSide sideFromShortForm:'l']] * 8; 
	
	chars[0] = 'G';
	chars[1] = charFromInt(sideValue);
	chars[2] = charFromInt([_colors count]-1);
	
	int charIndex = 3;
	
	for(int c = 0; c<[_colors count]; c++)
	{	
		TYColor *color = [_colors objectAtIndex:c];
		int colorValue = color.value*7;
		
		c++;
		
		if(c < [_colors count])
		{
			color = [_colors objectAtIndex:c];
			colorValue += color.value;
		}
		
		chars[charIndex++] = charFromInt(colorValue);
	}	
	
	chars[charIndex] = '\0';
}


+(PieceDecoder*) pieceDecoderFromEncodedChars: (char[]) chars
{
	
	int firstCharValue = intFromChar(chars[1]);
	int secondCharValue = intFromChar(chars[2]);
	
	NSMutableArray *sidesIn = [NSMutableArray array];
	
	if(firstCharValue >= 8)
	{
		[sidesIn addObject:[TYSide sideFromValue:3]];
		firstCharValue -=8;
	}
	
	if(firstCharValue >= 4)
	{
		[sidesIn addObject:[TYSide sideFromValue:2]];
		firstCharValue -= 4;
	}
	
	if(firstCharValue >= 2)
	{
		[sidesIn addObject:[TYSide sideFromValue:1]];
		firstCharValue -= 2;
	}
	
	if(firstCharValue >= 1)
	{
		[sidesIn addObject:[TYSide sideFromValue:0]];
	}
	
	int numColors = secondCharValue+1;
	
	NSMutableArray *colors = [NSMutableArray array];
	
	int c = 0;
	
	//two colors are packed into every char
	while ([colors count] < numColors) 
	{
		int charValue = intFromChar(chars[c+3]);
		[colors addObject:[TYColor colorFromValue:floor((float)charValue/7)]];
		
		if([colors count] < numColors) 
		{
			[colors addObject:[TYColor colorFromValue:charValue%7]];
		}
		
		c++;
	}
	
	GoalPiece *piece = [[[GoalPiece alloc] initWithColors:colors andSidesIn:sidesIn andCell:nil] autorelease];
	return [PieceDecoder pieceDecoderWithPiece:piece andNumCharsToRemove:c+3];
}

- (id)copyWithZone:(NSZone *)zone
{
	return  [[[self class] alloc] initWithColors:[[_colors mutableCopyWithZone:zone] autorelease] 
									  andSidesIn:[[_sidesIn mutableCopyWithZone:zone] autorelease] 
										 andCell:_cell];
}

-(NSString*) description
{
	
	//create a list of color chars
	char colorChars[[_colors count]];
	
	int c = 0;
	for(TYColor *color in _colors)
	{
		colorChars[c++] = color.shortForm;
	}
	colorChars[c] = '\0';
	
	//create a list of side in chars
	char sideInChars[[_sidesIn count]];
	
	int s = 0;
	for(TYSide *side in _sidesIn)
	{
		sideInChars[s++] = side.shortForm;
	}
	sideInChars[s] = '\0';
	 
	return [NSString stringWithFormat:@"{Piece %@ Colors:%s SidesIn:%s}", NSStringFromPieceType(_pieceType), colorChars, sideInChars];
}

-(void) dealloc
{
	[_colors release];
	[_sidesIn release];
	
	[super dealloc];
}


@end
