<script lang="ts">
  import { onMount } from "svelte";
  import { Canvas, Layer, t, type Render } from "svelte-canvas";
  import type { ServerState, XY } from "./types";

  const ROBOT_RADIUS = 0.18 * 1000;
  const BALL_RADIUS = 0.043 * 1000;

  let state: ServerState | null = null;
  onMount(() => {
    const interval = setInterval(async () => {
      const res = await fetch("/api/state");
      state = await res.json();
    }, 1000);

    return () => clearInterval(interval);
  });

  let render: Render;
  $: render = ({ context: ctx, width, height }) => {
    if (!state) return;
    const { own_players, opp_players, ball } = state.world;
    const { x: fieldW, y: fieldH } = state.world.field_dimensions;

    /**
     * Convert from server length to canvas length.
     */
    const convertLength = (length: number): number => {
      return Math.ceil(length * (width / fieldW));
    };

    /**
     * Convert from server coordinates to canvas coordinates.
     *
     * The server's coordinate system has its origin at the center of the field,
     * and its dimensions are given by `ServerState.world.field_dimension`.
     */
    const convertCoords = (coords: XY): XY => {
      const { x, y } = coords;

      return {
        x: (x + fieldW / 2) * (width / fieldW),
        y: (y + fieldH / 2) * (height / fieldH),
      };
    };

    // Draw field
    ctx.fillStyle = "#00aa00";
    ctx.clearRect(0, 0, width, height);
    ctx.fillRect(0, 0, width, height);

    // Draw field lines
    // TODO: Draw field lines

    // Draw ball
    const ballPos = convertCoords(ball.pos);
    const ballCanvasRadius = convertLength(BALL_RADIUS);
    console.log(ballPos);
    ctx.fillStyle = "red";
    ctx.beginPath();
    ctx.arc(ballPos.x, ballPos.y, ballCanvasRadius, 0, 2 * Math.PI);
    ctx.fill();

    // Draw players
    const drawPlayer = (serverPos: XY, color: string) => {
      const { x, y } = convertCoords(serverPos);
      const robotCanvasRadius = convertLength(ROBOT_RADIUS);
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(x, y, robotCanvasRadius, 0, 2 * Math.PI);
      ctx.fill();
    };
    own_players.forEach(({ pos }) => drawPlayer(pos, "blue"));
    opp_players.forEach(({ pos }) => drawPlayer(pos, "yellow"));
  };
</script>

<main class="cont">
  <Canvas width={840} height={600}>
    <Layer {render} />
  </Canvas>
</main>

<style>
  .cont {
    width: 100vw;
    height: 100vh;
  }
</style>
