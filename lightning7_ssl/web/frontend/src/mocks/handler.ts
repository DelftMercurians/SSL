import { rest } from "msw";
import type { ServerState } from "../types";

export const handlers = [
  rest.get("/api/poll", (req, res, ctx) => {
    const serverState: ServerState = {
      world: {
        ball: {
          pos: { x: 0, y: 0 },
          vel: { x: 0, y: 0 },
        },
        own_players: [
          {
            pos: { x: 0, y: 0 },
            vel: { x: 0, y: 0 },
          },
        ],
        opp_players: [
          {
            pos: { x: 0, y: 0 },
            vel: { x: 0, y: 0 },
          },
        ],
      },
      player_states: [
        {
          role: "goalie",
          target: { x: 0, y: 0 },
        },
      ],
    };
    return res(ctx.status(200), ctx.json(serverState));
  }),
];
