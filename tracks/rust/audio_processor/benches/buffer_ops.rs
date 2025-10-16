use criterion::{black_box, criterion_group, criterion_main, Criterion};
use audio_processor::unsafe_primitives::*;

fn bench_apply_gain(c: &mut Criterion) {
    let mut buffer = vec![0.5f32; 48000]; // 1 second @ 48kHz

    c.bench_function("apply_gain_unsafe", |b| {
        b.iter(|| {
            apply_gain_unsafe(black_box(&mut buffer), black_box(0.5));
        });
    });
}

fn bench_mix_buffers(c: &mut Criterion) {
    let mut dest = vec![0.5f32; 48000];
    let src = vec![0.25f32; 48000];

    c.bench_function("mix_buffers_unsafe", |b| {
        b.iter(|| {
            mix_buffers_unsafe(black_box(&mut dest), black_box(&src));
        });
    });
}

fn bench_convert_i16_to_f32(c: &mut Criterion) {
    let input = vec![16384i16; 48000];
    let mut output = vec![0.0f32; 48000];

    c.bench_function("convert_i16_to_f32_unsafe", |b| {
        b.iter(|| {
            convert_i16_to_f32_unsafe(black_box(&input), black_box(&mut output));
        });
    });
}

fn bench_convert_f32_to_i16(c: &mut Criterion) {
    let input = vec![0.5f32; 48000];
    let mut output = vec![0i16; 48000];

    c.bench_function("convert_f32_to_i16_unsafe", |b| {
        b.iter(|| {
            convert_f32_to_i16_unsafe(black_box(&input), black_box(&mut output));
        });
    });
}

fn bench_interleave_channels(c: &mut Criterion) {
    let ch1 = vec![0.5f32; 24000];
    let ch2 = vec![0.25f32; 24000];
    let channels: Vec<&[f32]> = vec![&ch1, &ch2];
    let mut output = vec![0.0f32; 48000];

    c.bench_function("interleave_channels_unsafe", |b| {
        b.iter(|| {
            interleave_channels_unsafe(black_box(&channels), black_box(&mut output));
        });
    });
}

fn bench_normalize(c: &mut Criterion) {
    let mut buffer = vec![0.5f32; 48000];
    buffer[1000] = 2.0; // Add a peak

    c.bench_function("normalize_unsafe", |b| {
        b.iter(|| {
            normalize_unsafe(black_box(&mut buffer));
        });
    });
}

fn bench_copy_buffer(c: &mut Criterion) {
    let src = vec![0.5f32; 48000];
    let mut dest = vec![0.0f32; 48000];

    c.bench_function("copy_buffer_unsafe", |b| {
        b.iter(|| {
            copy_buffer_unsafe(black_box(&src), black_box(&mut dest));
        });
    });
}

fn bench_clear_buffer(c: &mut Criterion) {
    let mut buffer = vec![0.5f32; 48000];

    c.bench_function("clear_buffer_unsafe", |b| {
        b.iter(|| {
            clear_buffer_unsafe(black_box(&mut buffer));
        });
    });
}

fn bench_compute_rms(c: &mut Criterion) {
    let buffer = vec![0.5f32; 48000];

    c.bench_function("compute_rms_unsafe", |b| {
        b.iter(|| {
            compute_rms_unsafe(black_box(&buffer));
        });
    });
}

fn bench_clip_buffer(c: &mut Criterion) {
    let mut buffer = vec![0.5f32; 48000];
    // Add some values that need clipping
    buffer[100] = 1.5;
    buffer[200] = -1.5;

    c.bench_function("clip_buffer_unsafe", |b| {
        b.iter(|| {
            clip_buffer_unsafe(black_box(&mut buffer));
        });
    });
}

criterion_group!(
    benches,
    bench_apply_gain,
    bench_mix_buffers,
    bench_convert_i16_to_f32,
    bench_convert_f32_to_i16,
    bench_interleave_channels,
    bench_normalize,
    bench_copy_buffer,
    bench_clear_buffer,
    bench_compute_rms,
    bench_clip_buffer
);

criterion_main!(benches);