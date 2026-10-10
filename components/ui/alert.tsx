import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const alertVariants = cva(
  "relative w-full rounded-xl border p-4 text-sm [&>svg~*]:pl-8 [&>svg+div]:translate-y-[-3px] [&>svg]:absolute [&>svg]:left-4 [&>svg]:top-4 [&>svg]:text-foreground transition-all duration-150",
  {
    variants: {
      variant: {
        default: "bg-background text-foreground border-border",
        destructive:
          "border-red-500/50 bg-red-950/20 text-red-200 dark:border-red-900/60 dark:bg-red-950/30 [&>svg]:text-red-400 shadow-[0_0_15px_rgba(239,68,68,0.1)]",
        warning:
          "border-amber-500/50 bg-amber-950/20 text-amber-200 dark:border-amber-900/60 dark:bg-amber-950/30 [&>svg]:text-amber-400 shadow-[0_0_15px_rgba(245,158,11,0.08)]",
        success:
          "border-emerald-500/50 bg-emerald-950/20 text-emerald-200 dark:border-emerald-900/60 dark:bg-emerald-950/30 [&>svg]:text-emerald-400",
        info:
          "border-cyan-500/40 bg-cyan-950/20 text-cyan-200 dark:border-cyan-900/60 dark:bg-cyan-950/30 [&>svg]:text-cyan-400",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

const Alert = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & VariantProps<typeof alertVariants>
>(({ className, variant, ...props }, ref) => (
  <div
    ref={ref}
    role="alert"
    className={cn(alertVariants({ variant }), className)}
    {...props}
  />
));
Alert.displayName = "Alert";

const AlertTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h5
    ref={ref}
    className={cn("mb-1 font-semibold leading-none tracking-tight text-foreground", className)}
    {...props}
  />
));
AlertTitle.displayName = "AlertTitle";

const AlertDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("text-xs leading-relaxed text-muted-foreground", className)}
    {...props}
  />
));
AlertDescription.displayName = "AlertDescription";

export { Alert, AlertTitle, AlertDescription };
