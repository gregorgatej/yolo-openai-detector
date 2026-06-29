# ADR 0001 — Product scope: single-image CPU object detection

Date: 2026-06-29

## Status

Accepted.

## Decision

The project is a CPU-only single-image object detection API.

It accepts one base64-encoded image and returns object detection results.

## In scope

- single image;
- object detection;
- bounding boxes;
- class labels;
- confidence scores;
- synchronous request-response API;
- OpenAI-compatible endpoint shape;
- fixed bearer API key;
- CPU-only inference.

## Out of scope

- object tracking;
- video;
- frame sequences;
- segmentation;
- masks;
- background jobs;
- queues;
- job IDs;
- polling;
- remote image URL fetching.

## Consequences

The service is smaller, easier to test, easier to run on GPU-less machines, and less likely to drift into an overbuilt analytics platform.
