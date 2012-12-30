//
//  GoalPiece.h
//  Trainyard
//
//  Created by Matt Rix on 09-10-03.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "Piece.h"
#import "DestinationPieceProtocol.h"

@class Cell;

@interface GoalPiece : Piece <DestinationPieceProtocol>
{
	NSMutableArray *_colors;
	NSMutableArray *_sidesIn;
}

@property (nonatomic, readwrite, retain) NSMutableArray *colors;
@property (nonatomic, readwrite, retain) NSMutableArray *sidesIn;

- (id)initWithColors:(NSMutableArray*)colors andSidesIn:(NSMutableArray*)sidesIn andCell:(Cell*)cell;
-(BOOL) isEmpty;

@end

@protocol GoalPieceDelegate <NSObject>

-(void)onGetTrain:(int)trainIndex;

@end

